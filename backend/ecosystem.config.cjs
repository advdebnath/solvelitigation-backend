module.exports = {
  apps: [
    {
      name: "sl-backend",
      script: "dist/server.js",
      cwd: "/var/www/solvelitigation/backend",
      exec_mode: "fork",
      instances: 1,
      time: true,

      env: {
        NODE_ENV: "production",
        MONGODB_URI: "mongodb://127.0.0.1:27017/solvelitigation",
        JWT_SECRET: "<<<KEEP YOUR REAL SECRET>>>",
      },
    },
  ],
};
