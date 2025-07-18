import axios from "axios";

import type { User, AuthResponse, LoginCredentials, SignupCredentials } from "../types/index";

const api = axios.create ({
    baseURL: "http://127.0.0.1:8000",
});

export const login = async (credentials: LoginCredentials) => {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    const response = await api.post<AuthResponse>('/login', formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    })
    return response.data;
};

export const signup = async (credentials: SignupCredentials) => {
    const response = await api.post<User>('/register', credentials);
    return response.data;
};