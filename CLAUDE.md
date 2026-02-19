# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a badminton/tennis court booking automation tool. It uses Selenium to automate form submission on jinshuju.com to reserve sports court slots.

## Commands

Run the main booking script with arguments:
```bash
python multi_jinze.py --usr "姓名" --phone "手机号" --num 人数 --type "羽毛球" --court 场地编号 --date 从今天开始第几天 --time 时间段序号
```

Run multiple bookings in parallel (for different users):
```bash
python jinze_rob.py
```

## Architecture

The project consists of two Python files:

- **multi_jinze.py** - Core automation script that:
  - Uses Selenium WebDriver with Chrome
  - Waits until a specified time before executing (configured in `pause()` function)
  - Fills in a web form on jinshuju.com with user info, phone, number of people, booking type
  - Selects court, date, and time slots
  - Submits the form automatically

- **jinze_rob.py** - Batch runner that launches multiple CMD windows, each running `multi_jinze.py` with different user parameters for parallel booking attempts

## Dependencies

- Selenium (`selenium` package)
- Pillow (`PIL` package)
- ChromeDriver (located at `C:/chromedriver-win64/chromedriver.exe`)

## Configuration

In `multi_jinze.py`:
- Line 60: Set the start time (`pause(driver, '09:00:00.175')`)
- Line 184: ChromeDriver path if needed

The script currently targets `https://jinshuju.com/f/vcswPJ` for form submission.
