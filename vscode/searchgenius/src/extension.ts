// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below


import * as vscode from 'vscode';

const configTarget = vscode.ConfigurationTarget.Global;

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "searchgenius" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let checkEndpoint = vscode.commands.registerCommand('searchgenius.checkEndpoint', () => {
		const configuration = vscode.workspace.getConfiguration("searchgenius");
		let  apiEndpoint = configuration.get("api.endpoint");
		vscode.window.showInformationMessage(`api.endpoint: ${apiEndpoint}`);
	});

	let openSettings = vscode.commands.registerCommand('searchgenius.openSettings', () => {
		vscode.commands.executeCommand("workbench.action.openSettings", "searchgenius.api.endpoint");
		vscode.window.showInformationMessage('Open Settings');
	});

	const view = vscode.window.registerWebviewViewProvider('searchgenius.webview', new SearchGeniusViewProvider(), {
        webviewOptions: {
            retainContextWhenHidden: true
        }
    });

	context.subscriptions.push(checkEndpoint, openSettings, view);
}

class SearchGeniusViewProvider implements vscode.WebviewViewProvider {
    private _view?: vscode.WebviewView;

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            // Enable scripts in the webview
            enableScripts: true
        };

        // Set the HTML content for the webview
        webviewView.webview.html = this.getHtmlForWebview(webviewView.webview);
    }

    private getHtmlForWebview(webview: vscode.Webview) {
        // Return HTML content with a button and a text box
        return `<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src ${webview.cspSource}; style-src ${webview.cspSource};">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                </head>
                <body>
                    <button id="myButton">Click Me!</button>
                    <textarea id="textBox" rows="4" cols="50"></textarea>

                    <script>
                        const button = document.getElementById('myButton');
                        const textBox = document.getElementById('textBox');

                        button.addEventListener('click', () => {
                            const randomText = 'Random Text: ' + Math.random().toString(36).substring(2, 15);
                            textBox.value += randomText + '\\n';
                        });
                    </script>
                </body>
                </html>`;
    }
}


// This method is called when your extension is deactivated
export function deactivate() {}
