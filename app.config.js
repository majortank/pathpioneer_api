module.exports = {
  apps: [
    {
      name: "fastapi-app",
      script: "main:app", // Replace with your actual script file and FastAPI app object
      interpreter: "python3", // Specify the Python interpreter
      instances: 1, // Number of application instances to be started
      autorestart: true, // Restart the application if it crashes
      watch: false, // Set to true if you want to watch for file changes and restart the app
      max_memory_restart: "1G", // Restart the app if it exceeds 1GB memory usage
      env: {
        NODE_ENV: "production", // Set the environment to production
      },
    },
  ],
};
