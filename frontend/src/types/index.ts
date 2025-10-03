export interface Structure {
  id: number;
  name: string;
  location: string;
  status: string;
  created_at?: string;
}

export interface SensorData {
  id: number;
  sensor_type: string;
  value: number;
  timestamp: string;
}
