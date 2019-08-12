import { createContext } from 'react';

export const WebSocketContext = createContext(new WebSocket('ws://localhost:8888'));
