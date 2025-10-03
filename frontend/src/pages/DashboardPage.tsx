import { useEffect, useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { getStructures } from '../api/structuresApi';
import { Structure } from '../types';
import {
  Container, Typography, Box, Paper, TableContainer, Table, TableHead, TableRow, TableCell, TableBody, Chip, CircularProgress, Alert, Button
} from '@mui/material';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

const DashboardPage = () => {
  const [structures, setStructures] = useState<Structure[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStructures = async () => {
      try {
        setLoading(true);
        const data = await getStructures();
        setStructures(data);
      } catch (err) {
        setError('Failed to fetch structures.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchStructures();
  }, []);

  const getStatusChipColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'operational': return 'success';
      case 'warning': return 'warning';
      case 'critical': return 'error';
      default: return 'default';
    }
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Infrastructure Dashboard
      </Typography>
      <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Structure Name</TableCell>
                <TableCell>Location</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {structures.map((structure) => (
                <TableRow key={structure.id}>
                  <TableCell>{structure.name}</TableCell>
                  <TableCell>{structure.location}</TableCell>
                  <TableCell>
                    <Chip label={structure.status} color={getStatusChipColor(structure.status)} />
                  </TableCell>
                  <TableCell align="right">
                    <Button
                      variant="outlined"
                      size="small"
                      component={RouterLink}
                      to={`/structures/${structure.id}`}
                      endIcon={<ArrowForwardIcon />}
                    >
                      View Details
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Container>
  );
};

export default DashboardPage;
