import React, { useState, useEffect } from 'react';
import { Box, Heading, Text, VStack, HStack, Divider, Spinner, Select,Input } from '@chakra-ui/react';
import apiClient from '../utils/http-common.js';
import WithSubnavigation from '../components/NavBar.tsx';
import useDocumentTitle from '../hooks/useDocumentTitle.js';

const PaymentHistoryItem = ({ payment }) => (
  <Box borderWidth="1px" borderRadius="lg" p={4} mb={4} boxShadow="md">
    <Heading size="md" color="teal.500">Payment #{payment.transaction_id}</Heading>
    <Text fontWeight="bold">Total Amount: ₦{parseFloat(payment.amount).toFixed(2)}</Text>
    <Text>Payment Date: {payment.payment_date}</Text>
    {/* <Text>Status: <span style={{color: loan.status === 'PENDING' ? 'orange' : 'green'}}>{loan.status}</span></Text>
    <Text>Repayment Date: {loan.repayment_date}</Text> */}
    
    <Divider my={2} />
    

  </Box>
);

const PaymentHistoryPage = () => {
  const [payments, setPayments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [sortBy, setSortBy] = useState('creation_date');
  const [searchTerm, setSearchTerm] = useState('');

  useDocumentTitle('Payment History')

  useEffect(() => {
    const fetchPaymentHistory = async () => {
      try {
        const response = await apiClient.get('/user-transactions/');
        setPayments(response.data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching payment history:', error);
        setIsLoading(false);
      }
    };

    fetchPaymentHistory();
  }, []);

  const sortPayment = (field) => {
    const sortedPayments = [...payments].sort((a, b) => {
      if (a[field] < b[field]) return -1;
      if (a[field] > b[field]) return 1;
      return 0;
    });
    setPayments(sortedPayments);
    setSortBy(field);
  };

  const filteredPayment = payments.filter(payment => 
    payment.transaction_id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return <Spinner size="xl" />;
  }
  

  return (
    <>
    <WithSubnavigation />
    <Box p={5}>
      <Heading mb={4}>Loan Payment History</Heading>
      <Input
        placeholder="Search by reference number"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        mb={4}
      />
      <HStack mb={4}>
        <Text>Sort by:</Text>
        <Select value={sortBy} onChange={(e) => sortPayment(e.target.value)}>
          <option value="payment_date">Payment Date</option>
          <option value="status">Status</option>
        </Select>
      </HStack>
      <VStack spacing={4} align="stretch">
        {filteredPayment.map(payment => (
          <PaymentHistoryItem key={payment.id} payment={payment} />
        ))}
      </VStack>
    </Box>
    </>
  );
};

export default PaymentHistoryPage;
