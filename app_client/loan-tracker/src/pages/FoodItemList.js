import React, { useState, useEffect } from 'react';
import { Box, Heading, Text, Button, SimpleGrid, VStack, HStack, Input, useToast, Container, Image, Badge, useColorModeValue , FormLabel} from '@chakra-ui/react';
import WithSubnavigation from '../components/NavBar.tsx';
import apiClient from '../utils/http-common.js';
import useDocumentTitle from '../hooks/useDocumentTitle.js';
import { motion } from 'framer-motion';

const FoodItem = ({ item, onAddToCart }) => {
  const [quantity, setQuantity] = useState(1);
  const bgColor = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  return (
    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
      <Box
        borderWidth="1px"
        borderRadius="lg"
        overflow="hidden"
        p={4}
        bg={bgColor}
        borderColor={borderColor}
        boxShadow="md"
      >
        <VStack align="start" spacing={2}>
          <Heading size="md">{item.name}</Heading>
          <Badge colorScheme="teal">₦{item.price}</Badge>
          <Text fontSize="sm" noOfLines={2}>{item.description}</Text>
          <HStack>
            <FormLabel>Quantity</FormLabel>
            <Input
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value)))}
              min={1}
              max={10}
              width="60px"
            />
            <Button colorScheme="teal" onClick={() => onAddToCart(item.id, quantity)}>
              Add to Cart
            </Button>
          </HStack>
        </VStack>
      </Box>
    </motion.div>
  );
};


const FoodItemList = () => {
  const [foodItems, setFoodItems] = useState([]);
  const toast = useToast();
  const bgColor = useColorModeValue('gray.50', 'gray.900');

  useEffect(() => {
    fetchFoodItems();
  }, []);

  const fetchFoodItems = async () => {
    try {
      const response = await apiClient.get('/food-items/');
      setFoodItems(response.data);
    } catch (error) {
      console.error('Error fetching food items:', error);
      toast({
        title: "Error",
        description: "Failed to fetch food items. Please try again later.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const handleAddToCart = async (foodItemId, quantity) => {
    try {
      await apiClient.post('/add-to-cart/', {
        food_item_id: foodItemId,
        quantity: quantity,
      });
      toast({
        title: "Success",
        description: "Item added to cart!",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      if (error.response && error.response.status === 401) {
        toast({
          title: "Error",
          description: "Please log in to add items to your cart.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      } else {
        console.error('Error adding item to cart:', error);
        toast({
          title: "Error",
          description: "Failed to add item to cart. Please try again.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      }
    }
  };

  useDocumentTitle('Food Items List');

  return (
    <>
      <WithSubnavigation />
      <Box bg={bgColor} minH="100vh" py={10}>
        <Container maxW={'7xl'}>
          <Heading as="h1" size="xl" mb={8} textAlign="center" color={useColorModeValue('teal.600', 'teal.300')}>
            Make a Loan Request
          </Heading>
          <Text fontSize="lg" textAlign="center" mb={10} color={useColorModeValue('gray.600', 'gray.400')}>
            Choose from our selection of items to request a loan.
          </Text>
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={10}>
            {foodItems.map((item) => (
              <FoodItem key={item.id} item={item} onAddToCart={handleAddToCart} />
            ))}
          </SimpleGrid>
        </Container>
      </Box>
    </>
  );
};

export default FoodItemList;
