import React from 'react';
import { Box, Flex, keyframes, useColorModeValue } from '@chakra-ui/react';

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const LoadingSpinner = () => {
  const spinnerColor = useColorModeValue('teal.500', 'teal.200');
  const bgColor = useColorModeValue('white', 'gray.800');

  return (
    <Flex height="100vh" alignItems="center" justifyContent="center" bg={bgColor}>
      <Box
        border="4px solid"
        borderColor={spinnerColor}
        borderTopColor="transparent"
        borderRadius="50%"
        width="100px"
        height="100px"
        animation={`${spin} 1s linear infinite`}
      />
    </Flex>
  );
};

export default LoadingSpinner;
