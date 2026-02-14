module.exports = {
  apps: [
    {
      name: "sl-backend",
      script: "dist/server.js",
      cwd: "/var/www/solvelitigation/backend",
      env: {
        NODE_ENV: "production",
        MONGODB_URI: "mongodb://sl_admin:solvelitigation%401966@127.0.0.1:27017/solvelitigation?authSource=admin",
        PORT: 4000,
      },
    },

    {
      name: "sl-ingestion-worker",
      script: "dist/workers/upload.worker.js",
      cwd: "/var/www/solvelitigation/backend",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "512M",
      env: {
        NODE_ENV: "production",
        MONGODB_URI: "mongodb://sl_admin:solvelitigation%401966@127.0.0.1:27017/solvelitigation?authSource=admin",
      },
    },
  ],
};
