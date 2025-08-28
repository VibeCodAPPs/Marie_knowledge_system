import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from '@/components/ui/toaster'
import Layout from '@/components/layout/Layout'
import Dashboard from '@/pages/Dashboard'
import Laboratory from '@/pages/Laboratory'
import MindMap from '@/pages/MindMap'
import Notebook from '@/pages/Notebook'
import Search from '@/pages/Search'

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/laboratory/:id" element={<Laboratory />} />
              <Route path="/mindmap/:laboratoryId" element={<MindMap />} />
              <Route path="/notebook/:laboratoryId" element={<Notebook />} />
              <Route path="/search" element={<Search />} />
            </Routes>
          </Layout>
          <Toaster />
        </div>
      </Router>
    </QueryClientProvider>
  )
}

export default App
