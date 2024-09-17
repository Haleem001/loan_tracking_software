import React, { useState, useEffect } from 'react';
import apiClient from '../utils/http-common.js';
import { Box, Heading, Text, Button, VStack, HStack, Divider, useToast, Container, Table, Thead, Tbody, Tr, Th, Td, useColorModeValue, Input } from '@chakra-ui/react';
import WithSubnavigation from '../components/NavBar.tsx';
import useDocumentTitle from '../hooks/useDocumentTitle.js';
import { motion } from 'framer-motion';

const LoanSuccessful = ({ loanDetails, onClose }) => {
  const cardBgColor = useColorModeValue('white', 'gray.700');
  const headingColor = useColorModeValue('teal.600', 'teal.300');
  const amountColor = useColorModeValue('teal.600', 'teal.300');

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      <Box p={8} maxWidth="800px" margin="auto" borderWidth={1} borderRadius="lg" boxShadow="xl" bg={cardBgColor}>
        <Heading mb={6} color={headingColor}>Loan Requested Successfully</Heading>
        <Text fontWeight="bold">Loan Reference Number: {loanDetails.reference_number}</Text>
        <VStack spacing={4} align="stretch" divider={<Divider />} mt={4}>
          {loanDetails.loan_items.map((item, index) => (
            <HStack key={index} justifyContent="space-between">
              <Text>{item.food_item_name}</Text>
              <Text>Quantity: {item.quantity}</Text>
              <Text fontWeight="semibold">₦{Number(item.price).toFixed(2)}</Text>
            </HStack>
          ))}
        </VStack>
        <Divider my={4} />
        <HStack justifyContent="space-between" mb={4}>
          <Text fontWeight="bold">Total Amount:</Text>
          <Text fontWeight="bold" fontSize="xl" color={amountColor}>₦{Number(loanDetails.total_amount).toFixed(2)}</Text>
        </HStack>
        <Button colorScheme="teal" size="lg" width="full" onClick={onClose}>
          Close
        </Button>
      </Box>
    </motion.div>
  );
};

const CartAndCheckout = () => {
  const [cartItems, setCartItems] = useState([]);
  const [repaymentDate, setRepaymentDate] = useState('');
  const [loanDetails, setLoanDetails] = useState(null);
  const toast = useToast();
  const bgColor = useColorModeValue('gray.50', 'gray.800');
  const cardBgColor = useColorModeValue('white', 'gray.700');
  const headingColor = useColorModeValue('teal.600', 'teal.300');
  const tableHeaderBg = useColorModeValue('gray.100', 'gray.700');
  const amountColor = useColorModeValue('teal.600', 'teal.300');

  useEffect(() => {
    fetchCartItems();
  }, []);

  const fetchCartItems = async () => {
    try {
      const response = await apiClient.get('/view-cart/');
      setCartItems(response.data);
    } catch (error) {
      console.error('Error fetching cart items:', error);
      toast({
        title: "Error",
        description: "Failed to fetch cart items. Please try again.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const handleCheckout = async () => {
    try {
      const response = await apiClient.post('/checkout/', {
        repayment_date: repaymentDate,
      });
      setLoanDetails(response.data);
      setCartItems([]);
      toast({
        title: "Checkout Successful",
        description: "Your loan has been created.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: "Checkout Failed",
        description: error.response?.data?.error || 'An error occurred during checkout',
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const totalAmount = cartItems.reduce((sum, item) => sum + Number(item.total_price), 0);
  useDocumentTitle('View Cart & Checkout');

  return (
    <>
      <WithSubnavigation />
      <Box bg={bgColor} minH="100vh" py={10}>
        <Container maxW={'7xl'}>
          {loanDetails ? (
            <LoanSuccessful loanDetails={loanDetails} onClose={() => setLoanDetails(null)} />
          ) : (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <Box borderWidth={1} borderRadius="lg" overflow="hidden" bg={cardBgColor} boxShadow="xl" p={6}>
                <Heading mb={6} color={headingColor}>Your Cart and Checkout</Heading>
                {cartItems.length > 0 ? (
                  <>
                    <Table variant="simple" mb={6}>
                      <Thead bg={tableHeaderBg}>
                        <Tr>
                          <Th>Item</Th>
                          <Th isNumeric>Quantity</Th>
                          <Th isNumeric>Price</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        {cartItems.map((item) => (
                          <Tr key={item.id}>
                            <Td>{item.food_item.name}</Td>
                            <Td isNumeric>{item.quantity}</Td>
                            <Td isNumeric>₦{Number(item.total_price).toFixed(2)}</Td>
                          </Tr>
                        ))}
                      </Tbody>
                    </Table>
                    <Divider my={4} />
                    <HStack justifyContent="space-between" mb={4}>
                      <Text fontWeight="bold">Total:</Text>
                      <Text fontWeight="bold" fontSize="xl" color={amountColor}>₦{totalAmount.toFixed(2)}</Text>
                    </HStack>
                    <VStack spacing={4} align="stretch">
                      <Input
                        type="date"
                        value={repaymentDate}
                        onChange={(e) => setRepaymentDate(e.target.value)}
                        placeholder="Repayment Date"
                      />
                      <Button colorScheme="teal" size="lg" onClick={handleCheckout}>
                        Complete Checkout
                      </Button>
                    </VStack>
                  </>
                ) : (
                  <Text textAlign="center" fontSize="lg">Your cart is empty.</Text>
                )}
              </Box>
            </motion.div>
          )}
        </Container>
      </Box>
    </>
  );
};

export default CartAndCheckout;
