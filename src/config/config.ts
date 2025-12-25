const config = {
  jwtSecret: process.env.JWT_SECRET || 'dev-secret',
  env: process.env.NODE_ENV || 'development',
};

export default config;
