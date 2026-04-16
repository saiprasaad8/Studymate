# Study Server Bot

A custom Discord bot built for managing and improving productivity in a study server.
This bot helps enforce focused study sessions, manage introductions, moderate spam, and welcome new members.


## Features

### Screen Share Enforcement
- When a user joins the study voice channel, they must start screen sharing.
- Timer: 2 minutes to start screen share.
- Alerts sent at:
  - 1 minute remaining
  - 15 seconds remaining
- If the user does not start screen sharing, they are removed from the voice channel.


### Welcome System
- Sends a welcome embed when a new member joins the server.
- Includes:
  - User avatar
  - Server name
  - Welcome message

### Moderation System
- Detects spam usage of `@everyone`.
- If a user mentions `@everyone` three times consecutively:
- User is timed out for 3 minutes

### Introduction Panel
- Interactive introduction system using buttons and modals.
- Users click **INTRODUCE** and fill a form.
- Their introduction is posted as an embed in the introduction channel.

### Announcement Command
Admin-only slash command to send announcements.

### Alert System Panel
- Interactive timer set system using buttons, modals and dropdown menu
- User clicks **Set Alert** button to set time, followed by a dropdown menu consists of Days in next ephemeral message
- The user can also view their aleet time and delete the current alert time using the **View Alert** and **Delete Alert** button
  
