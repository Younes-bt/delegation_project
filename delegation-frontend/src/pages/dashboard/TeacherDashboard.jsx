// delegation-frontend/src/pages/dashboard/teacher/TeacherDashboard.jsx
import { useState, useEffect } from 'react';
import api from '../../lib/axios';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../../components/ui/table';
import { Button } from '../../components/ui/button';

const TeacherDashboard = () => {
  const [trainings, setTrainings] = useState([]);
  const [distributions, setDistributions] = useState([]);
  const [trainingError, setTrainingError] = useState('');
  const [distributionError, setDistributionError] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const trainingResponse = await api.get('/accounts/trainings/me/');
        setTrainings(trainingResponse.data);
      } catch (err) {
        setTrainingError('Failed to load trainings: ' + (err.response?.data?.detail || err.message));
        console.error('Training API Error:', err);
      }
      try {
        const distResponse = await api.get('/training/annual-distributions/');
        setDistributions(distResponse.data);
      } catch (err) {
        setDistributionError('Failed to load weekly plans: ' + (err.response?.data?.detail || err.message));
        console.error('Distribution API Error:', err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Teacher Dashboard</h2>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <>
          <div className="mb-6">
            <h3 className="text-xl font-semibold mb-2">My Trainings</h3>
            {trainingError && <p className="text-red-500 mb-4">{trainingError}</p>}
            {trainings.length === 0 && !trainingError ? (
              <p>No trainings assigned.</p>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>
                    <TableHead>Description</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {trainings.map((training) => (
                    <TableRow key={training.id}>
                      <TableCell>{training.name || 'N/A'}</TableCell>
                      <TableCell>{training.description || 'N/A'}</TableCell>
                      <TableCell>
                        <Button variant="outline" size="sm">
                          View Details
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </div>

          <div>
            <h3 className="text-xl font-semibold mb-2">Weekly Plans</h3>
            {distributionError && <p className="text-red-500 mb-4">{distributionError}</p>}
            {distributions.length === 0 && !distributionError ? (
              <p>No plans available.</p>
            ) : (
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {distributions.map((dist) => (
                  <Card key={dist.id}>
                    <CardHeader>
                      <CardTitle>{dist.month_display} Week {dist.week || 'N/A'}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p><strong>Title:</strong> {dist.title || 'N/A'}</p>
                      <p><strong>Training:</strong> {dist.training || 'N/A'}</p>
                      <p><strong>Details:</strong> {dist.details || 'N/A'}</p>
                      <Button variant="outline" size="sm" className="mt-2">
                        View Plan
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default TeacherDashboard;
