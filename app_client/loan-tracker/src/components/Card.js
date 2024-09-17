// src/components/Card.js
import React from "react";
import { Box, Image, Text, Button, Stack } from "@chakra-ui/react";

const Card = ({ image, title, description, actionText, onAction }) => {
  return (
    <Box borderWidth="1px" borderRadius="lg" overflow="hidden">
      <Image src={image} alt={title} fallbackSrc='https://via.placeholder.com/150' />
      <Box p={5}>
        <Text fontWeight="bold" fontSize="xl" mb={2}>{title}</Text>
        <Text mb={4}>{description}</Text>
        {actionText && onAction && (
          <Button colorScheme="teal" onClick={onAction}>
            {actionText}
          </Button>
        )}
      </Box>
    </Box>
  );
};

export default Card;
