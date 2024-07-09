'use client';

import React from 'react';
import { useDjangoContext, User } from '../utils/djangoContext';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function Dashboard() {
  const user = useDjangoContext('user') as User | undefined;

  if (user === undefined) {
    return <div>Loading...</div>;
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Welcome</CardTitle>
        </CardHeader>
        <CardContent>
          {user ? (
            <div>
              <p>Hello, {user.username}!</p>
              <p>Email: {user.email}</p>
              <p>ID: {user.id}</p>
            </div>
          ) : (
            <p>Hello, Guest!</p>
          )}
        </CardContent>
      </Card>

      {/* Rest of your component */}
    </div>
  );
}
