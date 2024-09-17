import React, { useState, useEffect } from "react";
import { Box, Heading, Container, SimpleGrid, Stat, StatLabel, StatNumber, useColorModeValue, Text, Flex, Icon } from "@chakra-ui/react";
import WithSubnavigation from "../components/NavBar.tsx";
import useToken from "../hooks/useToken";
import apiClient from '../utils/http-common.js';
import useDocumentTitle from "../hooks/useDocumentTitle.js";
import { FaChartLine, FaCheckCircle, FaTimesCircle, FaDollarSign, FaMoneyBillWave, FaBalanceScale } from "react-icons/fa";

const StatCard = ({ title, stat, icon }) => {
  const borderColor = useColorModeValue('teal.500', 'teal.300');
  const bgColor = useColorModeValue('white', 'gray.700');
  
  return (
    <Stat
      px={{ base: 4, md: 8 }}
      py={'5'}
      shadow={'xl'}
      border={'1px solid'}
      borderColor={borderColor}
      rounded={'lg'}
      bg={bgColor}
      transition="all 0.3s"
      _hover={{ transform: 'translateY(-5px)', boxShadow: 'xl' }}
    >
      <Flex justifyContent="space-between" alignItems="center">
        <Box>
          <StatLabel fontWeight={'medium'} isTruncated>
            {title}
          </StatLabel>
          <StatNumber fontSize={'2xl'} fontWeight={'medium'}>
            {stat}
          </StatNumber>
        </Box>
        <Box
          my={'auto'}
          color={useColorModeValue('teal.500', 'teal.300')}
          alignContent={'center'}
        >
          <Icon as={icon} w={8} h={8} />
        </Box>
      </Flex>
    </Stat>
  );
};

const Home = () => {
  const { token } = useToken();
  const [dashboardData, setDashboardData] = useState(null);
  
  const bgColor = useColorModeValue('gray.50', 'gray.800');
  const headingColor = useColorModeValue('teal.600', 'teal.300');
  const textColor = useColorModeValue('gray.600', 'gray.400');

  useEffect(() => {
    const getDashboard = async () => {
      try {
        const response = await apiClient.get('/user-dashboard/');
        setDashboardData(response.data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        console.log(error.response.statusText);
      }
    };

    getDashboard();
  }, []);

  useDocumentTitle('Dashboard');

  return (
    <>
      <WithSubnavigation />
      {token && dashboardData ? (
        <Box bg={bgColor} minH="100vh" py={10}>
          <Container maxW={'7xl'}>
            <Heading as="h1" size="xl" mb={8} textAlign="center" color={headingColor}>
              User Dashboard
            </Heading>
            <Text fontSize="lg" textAlign="center" mb={10} color={textColor}>
              Welcome back! Here's an overview of your loan status.
            </Text>
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={{ base: 5, lg: 8 }}>
              <StatCard title="Loan Requests" stat={dashboardData.request} icon={FaChartLine} />
              <StatCard title="Approved Loans" stat={dashboardData.approved} icon={FaCheckCircle} />
              <StatCard title="Rejected Loans" stat={dashboardData.rejected} icon={FaTimesCircle} />
              <StatCard title="Total Loan Amount" stat={`₦${dashboardData.total_loan}`} icon={FaDollarSign} />
              <StatCard title="Total Paid Loan" stat={`₦${dashboardData.total_paid}`} icon={FaMoneyBillWave} />
              <StatCard title="Current Loan" stat={`₦${dashboardData.current_loan}`} icon={FaBalanceScale} />
            </SimpleGrid>
          </Container>
        </Box>
      ) : (
        <Box textAlign="center" py={10}>
          <Heading as="h2" size="xl" mt={6} mb={2}>
            Welcome to Our Loan Management System
          </Heading>
          <Text color={textColor}>
            Please log in to view your dashboard.
          </Text>
        </Box>
      )}
    </>
  );
};

export default Home;
