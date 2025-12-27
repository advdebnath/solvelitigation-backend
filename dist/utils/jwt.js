"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.signToken = signToken;
exports.verifyToken = verifyToken;
const jsonwebtoken_1 = __importDefault(require("jsonwebtoken"));
const config_1 = __importDefault(require("../config"));
function signToken(payload, secret = config_1.default.jwtSecret, expiresIn = "7d") {
    const options = { expiresIn };
    return jsonwebtoken_1.default.sign(payload, secret, options);
}
function verifyToken(token, secret = config_1.default.jwtSecret) {
    return jsonwebtoken_1.default.verify(token, secret);
}
