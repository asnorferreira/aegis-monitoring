import { AppBar, Toolbar, Typography, Button, Container, Box, Grid, Paper, Icon } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import MonitorHeartIcon from '@mui/icons-material/MonitorHeart';
import ShowChartIcon from '@mui/icons-material/ShowChart';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';

const LandingPage = () => {
  const features = [
    {
      icon: <MonitorHeartIcon fontSize="large" color="primary" />,
      title: 'Real-Time Monitoring',
      description: 'Continuously track the structural health of your assets with live sensor data feeds.',
    },
    {
      icon: <ShowChartIcon fontSize="large" color="primary" />,
      title: 'Predictive Analytics',
      description: 'Leverage data analytics to predict potential failures and schedule proactive maintenance.',
    },
    {
      icon: <NotificationsActiveIcon fontSize="large" color="primary" />,
      title: 'Instant Alerts',
      description: 'Receive immediate notifications for anomalies or critical events to ensure rapid response.',
    },
  ];

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Header */}
      <AppBar position="static" color="transparent" elevation={0} sx={{ borderBottom: '1px solid #ddd' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
            Aegis Monitoring
          </Typography>
          <Button color="inherit" component="a" href="#product">Product</Button>
          <Button color="inherit" component="a" href="#pricing">Pricing</Button>
          <Button color="inherit" component="a" href="#about">About Us</Button>
          <Button variant="outlined" component={RouterLink} to="/login" sx={{ ml: 2 }}>
            I'm already a client
          </Button>
        </Toolbar>
      </AppBar>

      {/* Hero Section */}
      <Container maxWidth="md" sx={{ textAlign: 'center', my: 10 }}>
        <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
          Ensuring Structural Integrity with Smart Monitoring
        </Typography>
        <Typography variant="h6" color="text.secondary" paragraph>
          Aegis provides a state-of-the-art platform for real-time monitoring of industrial infrastructures, turning complex data into actionable insights for engineers and asset managers.
        </Typography>
        <Button variant="contained" size="large" sx={{ mt: 3 }}>
          Request a Quote
        </Button>
      </Container>
      
      {/* Features Section */}
      <Box id="product" sx={{ py: 10, bgcolor: 'background.default' }}>
        <Container maxWidth="lg">
          <Typography variant="h4" component="h2" gutterBottom align="center" sx={{ mb: 6 }}>
            Platform Features
          </Typography>
          <Grid container spacing={4}>
            {features.map((feature) => (
              <Grid item xs={12} md={4} key={feature.title}>
                <Paper elevation={2} sx={{ p: 4, textAlign: 'center' }}>
                  <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                  <Typography variant="h6" gutterBottom>{feature.title}</Typography>
                  <Typography color="text.secondary">{feature.description}</Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Footer */}
      <Box component="footer" sx={{ bgcolor: 'primary.main', color: 'white', py: 6 }}>
        <Container maxWidth="lg">
          <Typography variant="body1" align="center">
            © {new Date().getFullYear()} Aegis Industrial Monitoring. All rights reserved.
          </Typography>
          <Typography variant="body2" align="center" sx={{ mt: 1 }}>
            Recife, Pernambuco, Brazil
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default LandingPage;
