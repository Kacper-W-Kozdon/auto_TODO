// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import {exec} from 'child_process';


// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "auto-todo" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	const disposable = vscode.commands.registerCommand('auto-todo.helloWorld', () => {
		// The code you place here will be executed every time your command is executed
		// Display a message box to the user
		vscode.window.showInformationMessage('Hello World from auto_todo!');
	});

	const runAutoTodo = vscode.commands.registerCommand('auto-todo.runAutoTodo', () => {
		const workspaceFolders = vscode.workspace.workspaceFolders;
		if (!workspaceFolders) {
			vscode.window.showErrorMessage('No workspace folder is open.');
			return;
		}

		const workspacePath = workspaceFolders[0].uri.fsPath;

		exec(`"TODO.py" ${workspacePath}`, { cwd: workspacePath }, (error, stdout, stderr) => {
			if (error) {
				vscode.window.showErrorMessage(`Error: ${error.message}`);
				return;
			}
			if (stderr) {
				vscode.window.showErrorMessage(`stderr: ${stderr}`);
				return;
			}
			vscode.window.showInformationMessage(`auto-todo completed:\n${stdout}`);
		});
	});

	context.subscriptions.push(disposable);
	context.subscriptions.push(runAutoTodo);
}

// This method is called when your extension is deactivated
export function deactivate() {}
