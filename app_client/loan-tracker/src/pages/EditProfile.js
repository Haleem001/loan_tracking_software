import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  useToast,
  Container,
  Divider,
} from '@chakra-ui/react';
import apiClient from '../utils/http-common';

const EditProfile = () => {
  const [first_name, setFirstName] = useState('');
  const [last_name, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const toast = useToast();

  useEffect(() => {
    const token = sessionStorage.getItem('token');
    if (token) {
      const decodedToken = decodeToken(token);
      setFirstName(decodedToken.first_name || '');
      setLastName(decodedToken.last_name || '');
      setEmail(decodedToken.email || '');
    }
  }, []);

  const decodeToken = (token) => {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    return JSON.parse(window.atob(base64));
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    try {
      await apiClient.put('/users/profile/', { first_name, email });
      toast({
        title: 'Profile updated',
        description: 'Your profile has been successfully updated.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to update profile: ' + error.response?.data?.message || error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      return toast({
        title: 'Error',
        description: 'New passwords do not match',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
    try {
      await apiClient.put('/users/change-password/', { currentPassword, newPassword });
      toast({
        title: 'Password changed',
        description: 'Your password has been successfully changed.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to change password: ' + error.response?.data?.message || error.message,
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Container maxW="container.md" py={10}>
      <VStack spacing={8} align="stretch">
        <Box>
          <Heading as="h2" size="lg" mb={4}>Edit Profile</Heading>
          <form onSubmit={handleProfileUpdate}>
            <VStack spacing={4}>
              <FormControl>
                <FormLabel htmlFor="name">Name</FormLabel>
                <Input
                  id="name"
                  value={first_name}
                  onChange={(e) => setFirstName(e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel htmlFor="name">Last Name</FormLabel>
                <Input
                  id="name"
                  value={last_name}
                  onChange={(e) => setLastName(e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel htmlFor="email">Email</FormLabel>
                <Input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </FormControl>
              <Button type="submit" colorScheme="teal">Update Profile</Button>
            </VStack>
          </form>
        </Box>

        <Divider />

        <Box>
          <Heading as="h2" size="lg" mb={4}>Change Password</Heading>
          <form onSubmit={handlePasswordChange}>
            <VStack spacing={4}>
              <FormControl>
                <FormLabel htmlFor="currentPassword">Current Password</FormLabel>
                <Input
                  id="currentPassword"
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel htmlFor="newPassword">New Password</FormLabel>
                <Input
                  id="newPassword"
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel htmlFor="confirmPassword">Confirm New Password</FormLabel>
                <Input
                  id="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </FormControl>
              <Button type="submit" colorScheme="teal">Change Password</Button>
            </VStack>
          </form>
        </Box>
      </VStack>
    </Container>
  );
};

export default EditProfile;
