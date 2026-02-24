module.exports = {
  apps: [
    {
      name: "sl-backend",
      script: "dist/server.js",
      cwd: "/var/www/solvelitigation/backend",
      instances: 1,
      exec_mode: "fork",
      autorestart: true,
      max_memory_restart: "500M",
      env: {
        NODE_ENV: "production",
        PORT: 4000
      }
    }
  ]
};
