import React, { useState, useEffect } from 'react';
import { Box, Heading, Text, VStack, HStack, Divider, Spinner, Select, Input } from '@chakra-ui/react';
import apiClient from '../utils/http-common.js';
import WithSubnavigation from '../components/NavBar.tsx';
import useDocumentTitle from '../hooks/useDocumentTitle.js';
const LoanHistoryItem = ({ loan }) => (
  <Box borderWidth="1px" borderRadius="lg" p={4} mb={4} boxShadow="md">
    <Heading size="md" color="teal.500">Loan #{loan.reference_number}</Heading>
    <Text fontWeight="bold">Total Amount: ₦{parseFloat(loan.total_amount).toFixed(2)}</Text>
    <Text>Creation Date: {loan.creation_date}</Text>
    <Text>Status: <span style={{color: loan.status === 'PENDING' ? 'orange' : 'green'}}>{loan.status}</span></Text>
    <Text>Repayment Date: {loan.repayment_date}</Text>
    
    <Divider my={2} />
    
    <Heading size="sm" mb={2}>Loan Items:</Heading>
    {loan.loan_items.map((item, index) => (
      <HStack key={index} justifyContent="space-between" bg="gray.50" p={2} borderRadius="md">
        <Text fontWeight="medium">{item.food_item_name}</Text>
        <Text>Quantity: {item.quantity}</Text>
        <Text>Price: ₦{parseFloat(item.price).toFixed(2)}</Text>
      </HStack>
    ))}
  </Box>
);

const LoanHistoryPage = () => {
  const [loans, setLoans] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [sortBy, setSortBy] = useState('creation_date');
  const [searchTerm, setSearchTerm] = useState('');

  useDocumentTitle('Loan History')

  useEffect(() => {
    const fetchLoanHistory = async () => {
      try {
        const response = await apiClient.get('/loan-history/');
        setLoans(response.data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching loan history:', error);
        setIsLoading(false);
      }
    };

    fetchLoanHistory();
  }, []);

  const sortLoans = (field) => {
    const sortedLoans = [...loans].sort((a, b) => {
      if (a[field] < b[field]) return -1;
      if (a[field] > b[field]) return 1;
      return 0;
    });
    setLoans(sortedLoans);
    setSortBy(field);
  };

  const filteredLoans = loans.filter(loan => 
    loan.reference_number.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return <Spinner size="xl" />;
  }



  return (
    <>
    <WithSubnavigation />
    <Box p={5}>
      <Heading mb={4}>Loan History</Heading>
      <Input
        placeholder="Search by reference number"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        mb={4}
      />
      <HStack mb={4}>
        <Text>Sort by:</Text>
        <Select value={sortBy} onChange={(e) => sortLoans(e.target.value)}>
          <option value="creation_date">Creation Date</option>
          <option value="repayment_date">Repayment Date</option>
          <option value="status">Status</option>
        </Select>
      </HStack>
      <VStack spacing={4} align="stretch">
        {filteredLoans.map(loan => (
          <LoanHistoryItem key={loan.id} loan={loan} />
        ))}
      </VStack>
    </Box>
    </>
  );
};

export default LoanHistoryPage;
