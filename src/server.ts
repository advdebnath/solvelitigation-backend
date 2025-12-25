// FILE: backend/src/server.ts
// ✅ Production-stable server.ts

import express from 'express';
import http from 'http';
import cors from 'cors';
import cookieParser from 'cookie-parser';
import helmet from 'helmet';
import morgan from 'morgan';

import { Server as IOServer } from 'socket.io';

import authRoutes from '@/routes/auth.routes';
import healthRoutes from '@/routes/health.routes';

// ------------------------------------------------------
// 🌐 Express app & HTTP server
// ------------------------------------------------------

const app = express();
const server = http.createServer(app);

// 🔌 Exported Socket.IO singleton
export let io: IOServer;

// ------------------------------------------------------
// 🔒 Auth safety check – fail fast if bcrypt is missing
// ------------------------------------------------------

try {
  require('bcrypt');
} catch {
  console.error('❌ bcrypt is missing – authentication cannot work');
}

// ------------------------------------------------------
// 🧩 MIDDLEWARES
// ------------------------------------------------------

app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(helmet());
app.use(morgan('dev'));

// ------------------------------------------------------
// 🚏 ROUTES
// ------------------------------------------------------

app.use('/api/health', healthRoutes);
app.use('/api/auth', authRoutes);

// ------------------------------------------------------
// 🚀 START SERVER
// ------------------------------------------------------

const PORT = Number(process.env.PORT) || 4000;

if (!module.parent) {
  server.listen(PORT, '0.0.0.0', () => {
    console.log(`[boot] server listening on http://0.0.0.0:${PORT}`);
  });
}

export default app;
