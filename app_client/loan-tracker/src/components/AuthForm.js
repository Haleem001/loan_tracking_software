// src/components/AuthForm.js
import React, { useState } from "react";
import { Box, Heading, Input, Button, Stack, Link, InputRightElement, InputGroup, Alert, AlertIcon, FormControl, FormLabel, InputLeftElement, IconButton } from "@chakra-ui/react";
import { useColorModeValue } from "@chakra-ui/react";
import { EmailIcon, LockIcon } from "@chakra-ui/icons";
import { useNavigate, useLocation } from 'react-router-dom';
import apiClient from "../utils/http-common";
import { motion } from "framer-motion";
import { FaEye, FaEyeSlash } from "react-icons/fa";

const AuthForm = ({ setToken }) => {
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [show, setShow] = useState(false);
  const handleClick = () => setShow(!show);
  const navigate = useNavigate();
  const location = useLocation();
  const [redirectTo] = useState(location.state?.from || '/');

  const handleSubmit = async () => {
    try {
      const response = await apiClient.post("users/authtoken/", { username, password });
      const token = response.data.access;
      const refreshToken = response.data.refresh;
      setToken(token);
      sessionStorage.setItem('refreshToken', refreshToken);
      navigate(redirectTo);
      window.location.reload();
    } catch (err) {
      console.error('ERROR', err);
      const messageer = err.response?.data?.detail || "An error occurred";
      setError(messageer);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Box
        rounded={'xl'}
        bg={useColorModeValue('white', 'gray.800')}
        boxShadow={'2xl'}
        p={8}
        maxWidth="400px"
        margin="auto"
        mt={10}
        backgroundImage={useColorModeValue(
          "linear-gradient(to bottom right, #ffffff, #f0f0f0)",
          "linear-gradient(to bottom right, #2d3748, #1a202c)"
        )}
      >
        <Heading mb={6} fontFamily="'Poppins', sans-serif" textAlign="center" fontSize="2xl">
          Welcome Back
        </Heading>
        <Stack spacing={4}>
          <FormControl>
            <FormLabel>Username</FormLabel>
            <InputGroup>
              <InputLeftElement children={<EmailIcon color="gray.500" />} />
              <Input
                placeholder="Username"
                value={username}
                onChange={(e) => setUserName(e.target.value)}
                _focus={{ borderColor: "teal.500", boxShadow: "0 0 0 1px teal.500" }}
              />
            </InputGroup>
          </FormControl>
          <FormControl>
            <FormLabel>Password</FormLabel>
            <InputGroup>
              <InputLeftElement children={<LockIcon color="gray.500" />} />
              <Input
                pr='4.5rem'
                type={show ? 'text' : 'password'}
                placeholder='Enter password'
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                _focus={{ borderColor: "teal.500", boxShadow: "0 0 0 1px teal.500" }}
              />
              <InputRightElement width='4.5rem'>
                <IconButton
                  h='1.75rem'
                  size='sm'
                  onClick={handleClick}
                  icon={show ? <FaEyeSlash /> : <FaEye />}
                  variant="ghost"
                />
              </InputRightElement>
            </InputGroup>
          </FormControl>
          <Link color="teal.500" href="/forgot-password" _hover={{ textDecoration: "underline" }}>Forgot Password?</Link>
          {error && (
            <Alert status="error" borderRadius="md">
              <AlertIcon />
              {error}
            </Alert>
          )}
          <Button
            colorScheme="teal"
            onClick={handleSubmit}
            mt={4}
            w="100%"
            _hover={{ bg: "teal.600" }}
            _active={{ bg: "teal.700" }}
            transition="all 0.2s"
          >
            Login
          </Button>
        </Stack>
      </Box>
    </motion.div>
  );
};

export default AuthForm;
