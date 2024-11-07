

import React, { useState } from 'react';
import apiClient from '../utils/http-common';
import { Box, Button, Input, Text, Heading, Stack } from '@chakra-ui/react';
import useDocumentTitle from '../hooks/useDocumentTitle';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiClient.post('users/forgot-password/', { email });
      setMessage('Password reset link sent to your email.');
    } catch (error) {
        const err_message = error.response.data.error
        
      setMessage(err_message);
    }
  };
  useDocumentTitle('Forgot Password')

  return (
    <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
    <Box p={5} textAlign="center">
      <Heading>Forgot Password</Heading>
      <form onSubmit={handleSubmit}>
        <Stack spacing={3} mt={4}>
          <Input
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="email"
          />
          <Button colorScheme="teal" type="submit">
            Send Password Reset Link
          </Button>
          {message && <Text>{message}</Text>}
        </Stack>
      </form>
    </Box>
    </Box>
  );
};

export default ForgotPassword;
