module.exports = {
  apps: [
    {
      name: "solvelitigation-backend",
      script: "dist/server.js",
      cwd: "/var/www/solvelitigation/backend",

      instances: 1,
      exec_mode: "fork",
      autorestart: true,
      watch: false,

      // ✅ Only non-secret runtime flags
      env: {
        NODE_ENV: "production",
      },
    },
  ],
};
