import React, {useEffect,useState}  from 'react';
import AppBar from '@mui/material/AppBar';
import CameraIcon from '@mui/icons-material/PhotoCamera';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import MemberScreen from '../MemberScreen/MemberScreen';
import ScienceIcon from '@mui/icons-material/Science';
import { w3cwebsocket as W3CWebSocket } from "websocket";
import {flow_1} from '../../Mock/MockFlow'
import {users} from '../../Mock/MockUsers'
import UserWindow from '../UserWindow/UserWindow';
function Copyright() {
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://mui.com/">
        Your Website
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}


const theme = createTheme();

export default function MainWindow() {
  const [flowSent,setFlowSent] = useState(false)
    useEffect(()=>{
      const ws = new W3CWebSocket('ws://127.0.0.1:7890');
      ws.onopen = ()=>{
      ws.send(JSON.stringify(flow_1))
      console.log("MainWindow::useEffect ~ sent flow to server")
      setFlowSent(true)
      }

    } ,[])
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="relative">
        <Toolbar>
          <ScienceIcon sx={{ mr: 2 }} />
          <Typography variant="h6" color="inherit" noWrap>
            Album layout
          </Typography>
        </Toolbar>
      </AppBar>
      <main>

        <Container sx={{ py: 8 }} maxWidth="xl">
          <Grid container spacing={4}>
            {
              flowSent?
              users.map((user) => (
              <Grid item key={user.id} xs={12} sm={6} md={4}>
                {/* <MemberScreen id={user} user={user}> </MemberScreen> */}
                <UserWindow workflow_id={flow_1.id}> </UserWindow>
              </Grid>
            )) :<div></div>
          }
          </Grid>
        </Container>
      </main>
      {/* Footer */}
      {/* <Box sx={{ bgcolor: 'background.paper', p: 6 }} component="footer">
        <Typography variant="h6" align="center" gutterBottom>
          Footer
        </Typography>
        <Typography
          variant="subtitle1"
          align="center"
          color="text.secondary"
          component="p"
        >
          Something here to give the footer a purpose!
        </Typography>
        <Copyright />
      </Box> */}
      {/* End footer */}
    </ThemeProvider>
  );
}