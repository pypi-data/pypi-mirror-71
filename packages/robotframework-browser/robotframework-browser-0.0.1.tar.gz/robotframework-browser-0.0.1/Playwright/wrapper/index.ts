import { IPlaywrightServer, PlaywrightService } from './generated/playwright_grpc_pb';
import { chromium, firefox, webkit, Browser, BrowserContext, Page } from 'playwright';
import {sendUnaryData, ServerUnaryCall, Server, ServerCredentials} from "grpc";
import {openBrowserRequest, Empty, Response, goToRequest, inputTextRequest, selectorRequest } from "./generated/playwright_pb";

// This is necessary for improved typescript inference
/* 
 * If obj is not trueish call callback with new Error containing message
 */
function exists<T1, T2>(obj: T1, callback: sendUnaryData<T2>, message: string): asserts obj is NonNullable<T1> {
    if (!obj) {
        callback(new Error(message), null)
    }
}

// Can't have an async constructor, this is a workaround
async function createBrowserState(browserType: string): Promise<BrowserState> {
    const headless = true 
    let browser, context, page
    if (browserType === 'firefox') {
        browser = await firefox.launch({headless: headless})
    } else if (browserType === 'chrome') {
        browser = await chromium.launch({headless: headless})
    } else if (browserType === 'webkit'){
        browser = await webkit.launch()
    } else {
        throw new Error("unsupported browser")
    }
    context = await browser.newContext()
    page = await context.newPage()
    return new BrowserState(browser, context, page)
}


class BrowserState {
    constructor(browser: Browser, context: BrowserContext, page: Page) {
        this.browser = browser
        this.context = context
        this.page = page
    }
    browser: Browser
    context: BrowserContext
    page: Page
}

function emptyWithLog(text: string): Response.Empty {
    const response = new Response.Empty()
    response.setLog(text)
    return response
}

class PlaywrightServer implements IPlaywrightServer {
    private browserState?: BrowserState
    // current open browsers main context and open page

    private async openUrlInPage(url: string, page: Page): Promise<string> {
        console.log('Go to url' + url)
        await page.goto(url)

        return "Succesfully opened URL " + url
    }

    async closeBrowser(call: ServerUnaryCall<Empty>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, "Tried to close browser but none was open")

        await this.browserState.browser.close()
        this.browserState = undefined
        console.log("Closed browser")
        const response = emptyWithLog('Closed browser')
        callback(null, response)
    }

    async openBrowser(call: ServerUnaryCall<openBrowserRequest>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        const browserType = call.request.getBrowser()
        const url = call.request.getUrl()
        console.log("Open browser: " + browserType)
        // TODO: accept a flag for headlessness
        this.browserState = await createBrowserState(browserType)
        const response = new Response.Empty()
        if (url) {
           const returnValue = await this.openUrlInPage(url, this.browserState?.page)
           response.setLog(returnValue);
        }
        console.log('Browser opened')
        callback(null, response);
    }

    async goTo(call: ServerUnaryCall<goToRequest>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        const url = call.request.getUrl()
        console.log("Go to URL: " + url)
        exists(this.browserState, callback, "Tried to open URl but had no browser open")
        await this.browserState.page.goto(url)
        const response = emptyWithLog("Succesfully opened URL")
        callback(null, response)
    }

    async getTitle(call: ServerUnaryCall<Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        exists(this.browserState, callback, "Tried to get title, no open browser")
        console.log('Getting title')
        const title = await this.browserState.page.title()
        const response = new Response.String()
        response.setBody(title)
        callback(null, response)
    }

    async getUrl(call: ServerUnaryCall<Empty>, callback: sendUnaryData<Response.String>): Promise<void> {
        exists(this.browserState, callback, "Tried to get page URL, no open browser")
        console.log('Getting URL')
        const url = this.browserState.page.url()
        const response = new Response.String()
        response.setBody(url)
        callback(null, response)
        
    }
    
    async getTextContent(call: ServerUnaryCall<selectorRequest>, callback: sendUnaryData<Response.String>): Promise<void> {
        exists(this.browserState, callback, "Tried to find text on page, no open browser")
        const selector = call.request.getSelector()
        const content = await this.browserState.page.textContent(selector)
        const response = new Response.String()
        response.setBody(content?.toString() || "")
        callback(null, response)
    }

    async getInputValue(call: ServerUnaryCall<selectorRequest>, callback: sendUnaryData<Response.String>): Promise<void> {
        exists(this.browserState, callback, "Tried to get input value, no open browser")
        const selector = call.request.getSelector()
        const element = await this.browserState.page.$(selector)
        exists(element, callback, "Couldn't find element: " + selector)
        // TODO: if this is done elsewhere write a helper function with error logging
        const property = await element.getProperty("value")
        const content = await property.jsonValue()
        const response = new Response.String()
        response.setBody(content)
        callback(null, response)
    }
    
    async inputText(call: ServerUnaryCall<inputTextRequest>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, "Tried to input text, no open browser")
        const inputText = call.request.getInput()
        const selector = call.request.getSelector()
        await this.browserState.page.fill(selector, inputText)
        
        const response = emptyWithLog("Input text: " + inputText)
        callback(null, response)
    }
    
    async clickButton(call: ServerUnaryCall<selectorRequest>, callback: sendUnaryData<Response.Empty>): Promise<void> {
        exists(this.browserState, callback, "Tried to click button, no open browser")

        const selector = call.request.getSelector()
        await this.browserState.page.click(selector)
        const response = emptyWithLog("Clicked button: " + selector)
        callback(null, response)
    }
}

const server = new Server();
server.addService<IPlaywrightServer>(PlaywrightService, new PlaywrightServer());
const port = process.env.PORT || '0'
server.bind(`localhost:${port}`, ServerCredentials.createInsecure());
console.log(`Listening on ${port}`);
server.start();
