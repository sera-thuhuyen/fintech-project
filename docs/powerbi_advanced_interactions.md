# Power BI Advanced Interactions Design

This document adds interactive features to make the Fintech Project Delivery Analytics dashboard feel more professional and portfolio-ready.

## Recommended Features

| Feature | Use Case | Pages |
| --- | --- | --- |
| Page navigation buttons | Move between dashboard pages without relying on page tabs. | All pages |
| Reset filters button | Quickly clear all slicer selections. | All pages |
| Slicer panel toggle | Show/hide slicers to maximize chart space. | All pages |
| Info/help bookmark panel | Explain KPI definitions and chart reading guidance. | All pages |
| Report page tooltips | Show rich details when hovering over project/department/employee. | Main chart pages |
| Drill-through pages | Open detail pages for Project, Department, or Employee. | Project Performance, Resource & Cost, Bottlenecks |
| Back button | Return from drill-through detail pages. | Drill-through pages |

## 1. Navigation Buttons

Create a small navigation strip at the top or left side of each page.

Recommended buttons:

```text
Overview
Projects
Resources
Bottlenecks
```

Button setup:

```text
Insert > Buttons > Blank
Action = On
Type = Page navigation
Destination = target page
```

Style:

```text
Default fill: #171C1B
Hover fill: #075E63
Selected/current page fill: #22C7D4
Text default: #FFFFFF
Text selected: #000000
Border: #075E63
```

Implementation note: Power BI does not automatically know the current selected page for button fill. Manually style the active page button differently on each page.

## 2. Reset Filters Button

Purpose: let users return the page to its default state.

Steps:

1. Set slicers to default state.
2. Go to `View > Bookmarks`.
3. Add bookmark:

```text
Reset - Page Name
```

4. In bookmark options, keep:

```text
Data = On
Display = On
Current page = On
```

5. Insert button:

```text
Insert > Buttons > Reset
```

6. Set action:

```text
Action = On
Type = Bookmark
Bookmark = Reset - Page Name
```

Recommended button label:

```text
Reset Filters
```

## 3. Slicer Panel Toggle

Purpose: hide slicers when users want more visual space.

Create two bookmarks per page:

```text
Slicers Show - Page Name
Slicers Hide - Page Name
```

Objects to include:

- slicer panel rectangle
- all slicers on the panel
- hide/show buttons

Steps:

1. Open `View > Selection` and `View > Bookmarks`.
2. Group slicer panel objects.
3. Create bookmark `Slicers Show` with group visible.
4. Hide slicer group in Selection pane.
5. Create bookmark `Slicers Hide` with group hidden.
6. Add two buttons:

```text
Filter icon button -> Bookmark: Slicers Show
Close/X button -> Bookmark: Slicers Hide
```

Recommended icons:

```text
Filter = show slicers
X = hide slicers
```

Style:

```text
Button fill: #075E63
Icon/text: #FFFFFF
Hover fill: #22C7D4
```

## 4. KPI Info / Help Panel Toggle

Purpose: explain KPIs without cluttering the dashboard.

Create a small info button near the page title.

Panel content examples:

```text
Budget Variance EUR = Actual Budget - Planned Budget
Schedule Delay Days = Actual End Date - Planned End Date
Task Hour Efficiency = Actual Hours / Planned Hours
```

Bookmarks:

```text
Info Show - Page Name
Info Hide - Page Name
```

Button:

```text
Insert > Buttons > Information
Action = Bookmark
```

Panel style:

```text
Background: #171C1B
Border: #075E63
Title: #22C7D4
Body text: #FFFFFF
```

## 5. Report Page Tooltips

Tooltips make charts feel much more polished.

### Tooltip Page: Project Tooltip

Create a new page:

```text
TT Project
```

Page settings:

```text
Page information > Tooltip = On
Canvas settings > Type = Tooltip
```

Recommended tooltip visuals:

- Project name / project ID
- Risk level
- Completion %
- Budget Variance EUR
- Schedule Delay Days
- Delayed Milestones
- Open Tasks

Use on visuals:

- Project Performance scatter
- Top Projects tables
- Bottleneck table

### Tooltip Page: Department Tooltip

Create:

```text
TT Department
```

Recommended tooltip visuals:

- Department name
- Total Projects
- Over Budget Projects
- Actual Labor Cost
- Avg Schedule Delay Days
- Delayed Milestones

Use on visuals:

- Department budget bar chart
- Delay by department chart
- Labor cost by department chart

### Tooltip Page: Employee Tooltip

Create:

```text
TT Employee
```

Recommended tooltip visuals:

- Employee name
- Role
- Experience level
- Hourly rate
- Actual task hours
- Actual labor cost
- Labor cost variance

Use on visuals:

- Hourly Rate vs Actual Hours scatter
- Employee Labor Detail matrix

## 6. Drill-Through Pages

Drill-through pages are strong portfolio features because they show deeper analysis flow.

### Drill-through Page: Project Detail

Create page:

```text
DT Project Detail
```

Drill-through field:

```text
dim_project[project_id]
```

Recommended visuals:

- KPI cards: Completion %, Budget Variance EUR, Schedule Delay Days, Delayed Milestones
- Task status breakdown
- Planned vs actual labor cost
- Milestone delay summary
- Project metadata table

Add back button:

```text
Insert > Buttons > Back
Action = Back
```

### Drill-through Page: Department Detail

Create page:

```text
DT Department Detail
```

Drill-through field:

```text
dim_department[department_name]
```

Recommended visuals:

- Projects by status
- Budget variance by project
- Actual labor cost by employee/role
- Delay metrics by project

### Drill-through Page: Employee Detail

Create page:

```text
DT Employee Detail
```

Drill-through field:

```text
dim_employee[employee_id]
```

Recommended visuals:

- Employee profile card
- Task list
- Planned vs actual hours
- Labor cost variance
- Projects assigned

## 7. Suggested Priority Order

Build in this order:

1. Page navigation buttons
2. Reset filters button
3. Slicer panel show/hide bookmarks
4. Project tooltip page
5. Project drill-through page
6. Department tooltip page
7. Employee tooltip/drill-through page
8. KPI info panel bookmarks

This order gives the most visible portfolio improvement with the least complexity first.

## 8. Naming Convention

Use clear names in Selection and Bookmarks panes.

Examples:

```text
BTN Nav Overview
BTN Nav Projects
BTN Reset Filters
BTN Show Slicers
BTN Hide Slicers
GRP Slicer Panel
GRP Info Panel
BM Show Slicers - Overview
BM Hide Slicers - Overview
BM Reset - Overview
TT Project
DT Project Detail
```

Good naming makes the report easier to maintain and explain in interviews.