import mongoose from 'mongoose';

const auditLogSchema = new mongoose.Schema({
  action: { type: String, required: true },
  judgmentId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Judgment',
    required: true,
  },
  status: String,
  error: String,
  retryCount: Number,
  triggeredBy: {
    type: String,
    enum: ['system', 'admin', 'cron'],
    default: 'system',
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

export const AuditLog = mongoose.model('AuditLog', auditLogSchema);
