`.vscode/launch.json`

``` json
{
	"version": "0.2.0",
	"configurations": [
	{
			"name": "WalletTrackerAPI",
			"type": "debugpy",
			"request": "launch",
			"module": "flask",
			"args": ["--app", "app:create_app", "run", "--debug"],
			"cwd": "${workspaceFolder}/app",
			"envFile": "${workspaceFolder}/.env",
			"python": "${workspaceFolder}/app/.venv/bin/python",
			"jinja": true
		}
	]
}
```