import type { SensorData, Structure } from '../types';
import axiosClient from './axiosClient';

export const getStructures = async (): Promise<Structure[]> => {
  const response = await axiosClient.get('/structures/');
  return response.data;
};

export const getStructureDetails = async (id: string): Promise<Structure> => {
  const response = await axiosClient.get(`/structures/${id}`);
  return response.data;
};

export const getSensorData = async (id: string): Promise<SensorData[]> => {
  const response = await axiosClient.get(`/structures/${id}/sensor-data`);
  return response.data;
};
