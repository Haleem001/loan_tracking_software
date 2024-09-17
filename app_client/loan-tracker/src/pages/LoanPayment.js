// src/pages/PaymentPage.js
import React, { useState, useEffect } from 'react';
import { Box, Button, Input, Text, Heading, Stack } from '@chakra-ui/react';
import createApiClient from '../utils/http-common.js';
import WithSubnavigation from '../components/NavBar.tsx';
const decodeToken = (token) => {
  const base64Url = token.split('.')[1];
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  return JSON.parse(window.atob(base64));
};

const PaymentPage = () => {
  const [amount, setAmount] = useState('');
  const [message, setMessage] = useState('');
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    const token = sessionStorage.getItem('token');
    if (token) {
      const decodedToken = decodeToken(token);
      setUserId(decodedToken.id);
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userId) {
      setMessage('User not authenticated. Please log in.');
      return;
    }
    try {
      const response = await createApiClient.post('/loan-payment/', {
        amount: amount,
        user: userId,
    
      });
      console.log(response)
      setMessage('Payment successful!');
      // Handle successful payment (e.g., redirect or show confirmation)
    } catch (error) {
      setMessage('Payment failed. Please try again.');
    }
  };

  return (
    <>
    <WithSubnavigation/>
 
    <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
      <Box p={5} textAlign="center">
        <Heading mb={4}>Make a Payment</Heading>
        <form onSubmit={handleSubmit}>
          <Stack spacing={3}>
            <Input
              placeholder="Enter amount"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              type="number"
              step="0.01"
            />
            <Button colorScheme="teal" type="submit">
              Submit Payment
            </Button>
            {message && <Text>{message}</Text>}
          </Stack>
        </form>
      </Box>
    </Box>
    </>
  );
};

export default PaymentPage;
