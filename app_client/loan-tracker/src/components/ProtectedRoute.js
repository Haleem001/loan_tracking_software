// src/components/ProtectedRoute.js
import React from "react";
import { Navigate } from "react-router-dom";
import useToken from "../hooks/useToken";

const ProtectedRoute = ({ element }) => {
  const { token } = useToken();

  if (!token) {
    return <Navigate to="/login" />;
  }

  return element;
};

export default ProtectedRoute;
