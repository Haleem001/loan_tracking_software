// src/pages/ResetPassword.js

import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Button, Input, Text, Heading, Stack } from '@chakra-ui/react';
import apiClient from '../utils/http-common';

const ResetPassword = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [message, setMessage] = useState('');
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== passwordConfirm) {
      setMessage('Passwords do not match.');
      return;
    }

    try {
      await apiClient.post(`/users/reset-password/${token}/`, {
        password
      });
      setMessage('Password reset successful. Redirecting to login...');
      setTimeout(() => navigate('/login'), 3000);
    } catch (error) {
      setMessage('Error resetting password.');
    }
  };

  return (
    <Box p={5} textAlign="center">
      <Heading>Reset Password</Heading>
      <form onSubmit={handleSubmit}>
        <Stack spacing={3} mt={4}>
          <Input
            placeholder="New password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
          />
          <Input
            placeholder="Confirm new password"
            value={passwordConfirm}
            onChange={(e) => setPasswordConfirm(e.target.value)}
            type="password"
          />
          <Button colorScheme="teal" type="submit">
            Reset Password
          </Button>
          {message && <Text>{message}</Text>}
        </Stack>
      </form>
    </Box>
  );
};

export default ResetPassword;
