import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getStructureDetails, getSensorData } from '../api/structuresApi';
import { Container, Typography, Box, Paper, Grid, CircularProgress, Alert, Chip } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import type { SensorData, Structure } from '../types';
import { format } from 'date-fns';

const StructureDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const [structure, setStructure] = useState<Structure | null>(null);
  const [sensorData, setSensorData] = useState<SensorData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

useEffect(() => {
    const fetchInitialData = async () => {
      if (!id) return;
      try {
        setLoading(true);
        const [details, sensor] = await Promise.all([
          getStructureDetails(id),
          getSensorData(id)
        ]);
        setStructure(details);
        setSensorData(sensor);
      } catch (err) {
        setError('Failed to fetch structure details.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchInitialData();

    const intervalId = setInterval(() => {
      if (id) {
        getSensorData(id)
          .then(newSensorData => {
            setSensorData(newSensorData);
            console.log("Sensor data refreshed");
          })
          .catch(err => {
            console.error("Failed to refresh sensor data:", err);
          });
      }
    }, 5000);

    return () => clearInterval(intervalId);
    
  }, [id]);

  
  const formatChartData = (type: string) => {
    return sensorData
      .filter(d => d.sensor_type === type)
      .map(d => ({
        timestamp: format(new Date(d.timestamp), 'HH:mm:ss'),
        value: d.value,
      }));
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!structure) return <Alert severity="info">Structure not found.</Alert>;
  
  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!structure) return <Alert severity="info">Structure not found.</Alert>;
  
  const getStatusChipColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'operational': return 'success';
      case 'warning': return 'warning';
      case 'critical': return 'error';
      default: return 'default';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Typography variant="h4" gutterBottom sx={{ mb: 0, mr: 2 }}>
          {structure.name}
        </Typography>
        <Chip label={structure.status} color={getStatusChipColor(structure.status)} />
      </Box>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Localização: {structure.location}
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {['Vibration', 'Strain', 'Temperature'].map(type => (
          <Grid item xs={12} key={type}>
            <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 300 }}>
              <Typography variant="h6">{type} Data</Typography>
              <ResponsiveContainer>
                <LineChart data={formatChartData(type)} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="timestamp" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default StructureDetailPage;