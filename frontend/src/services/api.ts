import axios from "axios";

import type { User, AuthResponse, LoginCredentials, SignupCredentials } from "../types";

const api = axios.create ({
    baseURL: "http://localhost:8000",
});

export const login = async (credentials: LoginCredentials) => {
    const response = await api.post<AuthResponse>('/login', credentials);
    return response.data;
};

export const signup = async (credentials: SignupCredentials) => {
    const response = await api.post<User>('/signup', credentials);
    return response.data;
};