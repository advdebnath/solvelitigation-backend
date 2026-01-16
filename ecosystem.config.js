module.exports = {
  apps: [
    {
      name: "solvelitigation-backend",
      script: "dist/server.js",
      cwd: "/var/www/solvelitigation/backend",
      instances: 1,
      exec_mode: "fork",
      env: {
        NODE_ENV: "development",
        PORT: 4000,
        MONGO_URI: "mongodb://127.0.0.1:27017/solvelitigation",
        JWT_SECRET: "dev-secret"
      },
      env_production: {
        NODE_ENV: "production",
        PORT: 4000,
        MONGO_URI: "mongodb://127.0.0.1:27017/solvelitigation",
        JWT_SECRET: "solvelitigation-secret-key-change-in-production"
      }
    }
  ]
};
