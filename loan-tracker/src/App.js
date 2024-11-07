// src/App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ChakraProvider, ColorModeScript } from "@chakra-ui/react";
import LoginSignup from "./pages/LoginSignup";
import Home from "./pages/Home";
import ProtectedRoute from "./components/ProtectedRoute";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import FoodItemList from "./pages/FoodItemList";
import CartAndCheckout from "./pages/CartAndCheckout";
import NotFound from "./pages/NotFound";
import LoanHistoryPage from "./pages/LoanHistory";
import PaymentPage from "./pages/LoanPayment";
import PaymentHistoryPage from "./pages/PaymentHistory";
import theme from './theme'
import LoadingSpinner from './components/LoadingSpinner';
import EditProfile from './pages/EditProfile';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  
    useEffect(() => {
      // Simulate loading time or fetch initial data
      setTimeout(() => {
        setIsLoading(false);
      }, 1000);
    }, []);
  
    if (isLoading) {
      return <LoadingSpinner />;
    }
  return (
    <ChakraProvider theme={theme}>
      <ColorModeScript initialColorMode={theme.config.initialColorMode} />
       {isLoading ? (
              <LoadingSpinner />
            ) : (
            <Router>
        <Routes>
          <Route path="/" element={<ProtectedRoute element={<Home />} />} />
          <Route path="/login" element={<LoginSignup />} />
          <Route path="*" element={<NotFound />} />
          <Route path="/food-items" element={<ProtectedRoute element={<FoodItemList />} /> } />
          <Route path="/view-cart" element={<ProtectedRoute element={<CartAndCheckout />} />} />
          <Route path="/loan-request-history" element={<ProtectedRoute element={<LoanHistoryPage />} />} />
          <Route path="/loan-payment-history" element={<ProtectedRoute element={<PaymentHistoryPage/>} />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/loan-payment" element={<ProtectedRoute element={<PaymentPage />} />} />
        <Route path="/reset-password/:token" element={<ResetPassword />} />
        <Route path='edit-profile' element={<ProtectedRoute element={<EditProfile />} />} />
        </Routes>
      </Router>   
            )}
     
    </ChakraProvider>
  );
}

export default App;
