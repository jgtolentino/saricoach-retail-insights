import { test, expect } from "@playwright/test";

test("home page shows KPIs and coach suggestions", async ({ page }) => {
    await page.goto("/");

    // Wait for KPI cards to load
    // We look for "Daily Sales" which is a label in KpiCard
    // Use exact: true to avoid matching "daily sales" in coach suggestions
    await expect(page.getByText("Daily Sales", { exact: true })).toBeVisible({ timeout: 10000 });

    // Coach panel title
    await expect(page.getByText("Coach Suggestions")).toBeVisible();

    // At least one suggestion rendered in the list
    // The CoachPanel renders items in a simple div structure, let's look for text content or structure
    // Based on CoachPanel.tsx, it renders:
    // <div className="space-y-3">
    //   {coach.actions.map(...)}
    // </div>

    // We can check if "Action" label exists (it's part of the item rendering)
    // CoachPanel renders a list of actions
    // <ul className="list-disc ...">
    //   <li>...</li>
    // </ul>
    await expect(page.locator("ul li").first()).toBeVisible();
});
