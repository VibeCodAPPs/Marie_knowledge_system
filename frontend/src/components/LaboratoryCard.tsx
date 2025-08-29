import React from 'react';
import { Laboratory } from '../types/laboratory';
import Button from './ui/Button';

interface LaboratoryCardProps {
  laboratory: Laboratory;
  onSelect: (laboratory: Laboratory) => void;
  onEdit?: (laboratory: Laboratory) => void;
  onDelete?: (laboratory: Laboratory) => void;
}

const LaboratoryCard: React.FC<LaboratoryCardProps> = ({
  laboratory,
  onSelect,
  onEdit,
  onDelete
}) => {
  const handleCardClick = () => {
    onSelect(laboratory);
  };

  const handleEditClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    onEdit?.(laboratory);
  };

  const handleDeleteClick = (e: React.MouseEvent) => {
    e.stopPropagation();
    onDelete?.(laboratory);
  };

  return (
    <div 
      className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer border-l-4 p-6"
      style={{ borderLeftColor: laboratory.color }}
      onClick={handleCardClick}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <span className="text-2xl">{laboratory.icon}</span>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {laboratory.name}
            </h3>
            {!laboratory.is_active && (
              <span className="inline-block px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded-full">
                Inactive
              </span>
            )}
          </div>
        </div>
        
        {/* Actions */}
        <div className="flex space-x-2">
          {onEdit && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleEditClick}
              className="text-gray-500 hover:text-gray-700"
            >
              ✏️
            </Button>
          )}
          {onDelete && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleDeleteClick}
              className="text-red-500 hover:text-red-700"
            >
              🗑️
            </Button>
          )}
        </div>
      </div>

      {/* Description */}
      {laboratory.description && (
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
          {laboratory.description}
        </p>
      )}

      {/* Statistics */}
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="text-center">
          <div className="text-lg font-semibold text-blue-600">
            {laboratory.concept_count || 0}
          </div>
          <div className="text-xs text-gray-500">Concepts</div>
        </div>
        <div className="text-center">
          <div className="text-lg font-semibold text-green-600">
            {laboratory.source_count || 0}
          </div>
          <div className="text-xs text-gray-500">Sources</div>
        </div>
        <div className="text-center">
          <div className="text-lg font-semibold text-purple-600">
            {Math.floor((laboratory.study_hours || 0) / 60)}h
          </div>
          <div className="text-xs text-gray-500">Study Time</div>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
        <div 
          className="h-2 rounded-full transition-all duration-300"
          style={{ 
            width: `${Math.min(100, (laboratory.concept_count || 0) * 2)}%`,
            backgroundColor: laboratory.color 
          }}
        />
      </div>
      
      {/* Footer */}
      <div className="flex justify-between items-center text-xs text-gray-500">
        <span>
          Updated {new Date(laboratory.updated_at || '').toLocaleDateString()}
        </span>
        <span className="flex items-center space-x-1">
          <span>🎯</span>
          <span>Active Learning</span>
        </span>
      </div>
    </div>
  );
};

export default LaboratoryCard;
