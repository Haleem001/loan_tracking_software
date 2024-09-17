// src/hooks/useToken.js
import { useState } from "react";

function useToken() {
  const getToken = () => {
    return sessionStorage.getItem("token");
  };

  const [token, setToken] = useState(getToken());

  const saveToken = (userToken) => {
    sessionStorage.setItem("token", userToken);
    setToken(userToken);
  };

  const removeToken = () => {
    sessionStorage.removeItem("token");
    setToken(null);
  };

  return {
    setToken: saveToken,
    removeToken,
    token
  };
}

export default useToken;
