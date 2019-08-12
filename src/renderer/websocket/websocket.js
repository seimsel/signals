import { createContext } from 'react';

const ws = new WebSocket('ws://localhost:8888')
const WebSocketContext = createContext(ws);

export default WebSocketContext;
