// src/pages/LoginSignup.js
import React from "react";
import { Box } from "@chakra-ui/react";
import AuthForm from "../components/AuthForm";
import useToken from "../hooks/useToken";
import useDocumentTitle from "../hooks/useDocumentTitle";
import WithSubnavigation from "../components/NavBar.tsx";

const LoginSignup = () => {
  const { setToken } = useToken();
  useDocumentTitle('Login');

  return (
    <>
    <WithSubnavigation />
    
    <Box display="flex" justifyContent="center" alignItems="center" height="100vh" >
      <AuthForm setToken={setToken} />
    </Box>
    
    </>
  );
};

export default LoginSignup;
