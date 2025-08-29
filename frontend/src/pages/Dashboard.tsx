import React, { useState, useEffect } from 'react';
import { Laboratory } from '../types/laboratory';
import LaboratoryCard from '../components/LaboratoryCard';
import Button from '../components/ui/Button';

const Dashboard: React.FC = () => {
  const [laboratories, setLaboratories] = useState<Laboratory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Mock data for Phase 1 - replace with API calls later
  useEffect(() => {
    const mockLaboratories: Laboratory[] = [
      {
        id: 1,
        name: "Artificial Intelligence",
        description: "Machine Learning, Deep Learning, and AI applications",
        color: "#3B82F6",
        icon: "🤖",
        is_active: true,
        is_archived: false,
        settings: {},
        concept_count: 24,
        source_count: 12,
        study_hours: 180,
        created_at: "2024-01-15T10:00:00Z",
        updated_at: "2024-01-20T15:30:00Z",
        display_name: "🤖 Artificial Intelligence"
      },
      {
        id: 2,
        name: "Philosophy",
        description: "Stoicism, Ethics, and Modern Philosophy",
        color: "#8B5CF6",
        icon: "🏛️",
        is_active: true,
        is_archived: false,
        settings: {},
        concept_count: 18,
        source_count: 8,
        study_hours: 120,
        created_at: "2024-01-10T09:00:00Z",
        updated_at: "2024-01-18T14:20:00Z",
        display_name: "🏛️ Philosophy"
      },
      {
        id: 3,
        name: "Physics",
        description: "Quantum Mechanics and Theoretical Physics",
        color: "#10B981",
        icon: "⚛️",
        is_active: false,
        is_archived: false,
        settings: {},
        concept_count: 6,
        source_count: 4,
        study_hours: 45,
        created_at: "2024-01-05T08:00:00Z",
        updated_at: "2024-01-12T11:15:00Z",
        display_name: "⚛️ Physics"
      }
    ];

    // Simulate API loading
    setTimeout(() => {
      setLaboratories(mockLaboratories);
      setLoading(false);
    }, 1000);
  }, []);

  const handleSelectLaboratory = (laboratory: Laboratory) => {
    console.log('Selected laboratory:', laboratory);
    // Navigate to laboratory detail page
    // router.push(`/laboratory/${laboratory.id}`);
  };

  const handleEditLaboratory = (laboratory: Laboratory) => {
    console.log('Edit laboratory:', laboratory);
    // Open edit modal or navigate to edit page
  };

  const handleDeleteLaboratory = (laboratory: Laboratory) => {
    console.log('Delete laboratory:', laboratory);
    // Show confirmation dialog and delete
  };

  const handleCreateLaboratory = () => {
    console.log('Create new laboratory');
    // Open create modal or navigate to create page
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading laboratories...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <p className="text-red-600 mb-4">Error: {error}</p>
          <Button onClick={() => window.location.reload()}>
            Retry
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Marie's Laboratories
              </h1>
              <p className="text-gray-600 mt-1">
                Organize your knowledge into focused domains
              </p>
            </div>
            <Button onClick={handleCreateLaboratory}>
              ➕ New Laboratory
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Statistics Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <span className="text-2xl">🧪</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Labs</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {laboratories.length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <span className="text-2xl">💡</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Concepts</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {laboratories.reduce((sum, lab) => sum + lab.concept_count, 0)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <span className="text-2xl">📚</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Sources</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {laboratories.reduce((sum, lab) => sum + lab.source_count, 0)}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="p-2 bg-orange-100 rounded-lg">
                <span className="text-2xl">⏱️</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Study Hours</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {Math.floor(laboratories.reduce((sum, lab) => sum + lab.study_hours, 0) / 60)}h
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Laboratories Grid */}
        {laboratories.length === 0 ? (
          <div className="text-center py-12">
            <span className="text-6xl mb-4 block">🧪</span>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No laboratories yet
            </h3>
            <p className="text-gray-600 mb-6">
              Create your first laboratory to start organizing your knowledge
            </p>
            <Button onClick={handleCreateLaboratory}>
              Create Laboratory
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {laboratories.map((laboratory) => (
              <LaboratoryCard
                key={laboratory.id}
                laboratory={laboratory}
                onSelect={handleSelectLaboratory}
                onEdit={handleEditLaboratory}
                onDelete={handleDeleteLaboratory}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
