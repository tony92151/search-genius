// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below


import {
	ConfigurationTarget,
	InputBoxValidationSeverity,
	ProgressLocation,
	Uri,
	ThemeIcon,
	ExtensionContext,
	workspace,
	window,
	env,
	commands,
  } from "vscode";

const configTarget = ConfigurationTarget.Global;

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "searchgenius" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let checkEndpoint = commands.registerCommand('searchgenius.checkEndpoint', () => {
		const configuration = workspace.getConfiguration("searchgenius");
		let  apiEndpoint = configuration.get("api.endpoint");
		window.showInformationMessage(`api.endpoint: ${apiEndpoint}`);
	});

	let openSettings = commands.registerCommand('searchgenius.openSettings', () => {
		commands.executeCommand("workbench.action.openSettings", "searchgenius.api.endpoint");
		window.showInformationMessage('Open Settings');
	});

	context.subscriptions.push(checkEndpoint, openSettings);
}

// This method is called when your extension is deactivated
export function deactivate() {}
