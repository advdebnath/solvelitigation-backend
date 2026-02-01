module.exports = {
  apps: [
    {
      name: "sl-backend",
      script: "dist/server.js",
      cwd: "/var/www/solvelitigation/backend",
      env: {
        NODE_ENV: "production",
        MONGODB_URI: "mongodb://127.0.0.1:27017/solvelitigation",
        PORT: 4000
      }
    }
  ]
};
