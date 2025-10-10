// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from "vscode";
import { exec } from "child_process";

let path = require("path");

class Extension {
  debug: boolean;

  constructor() {
    this.debug = false;
  }
}

let extension = new Extension();

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
  // Use the console to output diagnostic information (console.log) and errors (console.error)
  // This line of code will only be executed once when your extension is activated
  console.log('Congratulations, your extension "auto-todo" is now active!');

  // The command has been defined in the package.json file
  // Now provide the implementation of the command with registerCommand
  // The commandId parameter must match the command field in package.json
  const disposable = vscode.commands.registerCommand(
    "auto-todo.helloWorld",
    () => {
      // The code you place here will be executed every time your command is executed
      // Display a message box to the user
      vscode.window.showInformationMessage("Hello World from auto_todo!");
    }
  );

  let debugExtension = vscode.commands.registerCommand(
    "auto-todo.debug",
    () => {
      extension.debug = !extension.debug;
      console.log(`Debug: ${!extension.debug} -> ${extension.debug}`);
      vscode.window.showInformationMessage(
        `Debug: ${!extension.debug} -> ${extension.debug}`
      );
      return extension.debug;
    }
  );

  const runAutoTodo = vscode.commands.registerCommand(
    "auto-todo.runAutoTodo",
    () => {
      const workspaceFolders = vscode.workspace.workspaceFolders;
      if (!workspaceFolders) {
        vscode.window.showErrorMessage("No workspace folder is open.");
        return;
      }

      const extensionPath = path.join(__dirname, "../../src/TODO");

      const workspacePath = workspaceFolders[0].uri.fsPath;

      console.log(
        `Entered "auto-todo.runAutoTodo". CWD: ${workspacePath}, extension script directory: ${extensionPath}`
      );
      vscode.window.showInformationMessage('Entered "auto-todo.runAutoTodo"');

      exec(
        `python ${extensionPath}\\TODO.py --debug ${extension.debug.toString()} '${workspacePath}'`,
        // ["", `${workspacePath}\\testTODOplaceholer.py`],
        // { cwd: workspacePath },
        (error, stdout, stderr) => {
          if (error) {
            vscode.window.showErrorMessage(`Error: ${error.message}`);
            console.log(`Error: ${error.message}`);
            return;
          }
          if (stderr) {
            vscode.window.showErrorMessage(`stderr: ${stderr}`);
            console.log(`stderr: ${stderr}`);
            return;
          }
          vscode.window.showInformationMessage(
            `auto-todo completed:\n${stdout}`
          );
          console.log(`auto-todo completed:\n${stdout}`);
        }
      );
    }
  );

  context.subscriptions.push(disposable);
  context.subscriptions.push(runAutoTodo);
  context.subscriptions.push(debugExtension);
}

// This method is called when your extension is deactivated
export function deactivate() {}
