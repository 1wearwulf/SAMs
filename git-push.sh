#!/bin/bash

# Git push script for SAMS project

echo "🚀 Preparing to push SAMS project to GitHub..."
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if we're in the right directory
if [ ! -f "start-project.sh" ]; then
    echo -e "${RED}Error: Not in sams-project root directory${NC}"
    echo "Navigate to: ~/Documents/blackb/sams-project"
    exit 1
fi

# Check git status
echo -e "${BLUE}Checking git status...${NC}"
git status

echo ""
echo -e "${YELLOW}Do you want to:${NC}"
echo "1. Commit and push all changes"
echo "2. Only push existing commits"
echo "3. Set up new GitHub remote"
echo "4. Exit"
echo ""
read -p "Enter choice (1-4): " choice

case $choice in
    1)
        # Commit and push
        echo -e "${BLUE}Staging all changes...${NC}"
        git add .
        
        echo -e "${BLUE}Enter commit message:${NC}"
        read commit_msg
        
        if [ -z "$commit_msg" ]; then
            commit_msg="Update SAMS project - $(date '+%Y-%m-%d %H:%M:%S')"
        fi
        
        echo -e "${BLUE}Committing: $commit_msg${NC}"
        git commit -m "$commit_msg"
        
        echo -e "${BLUE}Pushing to GitHub...${NC}"
        git push origin main
        ;;
        
    2)
        # Push only
        echo -e "${BLUE}Pushing to GitHub...${NC}"
        git push origin main
        ;;
        
    3)
        # Set up new remote
        echo -e "${BLUE}Current remotes:${NC}"
        git remote -v
        
        echo ""
        echo -e "${YELLOW}Enter your GitHub repository URL:${NC}"
        echo "Example: https://github.com/username/sams-project.git"
        read github_url
        
        if [ -n "$github_url" ]; then
            # Remove existing origin if any
            git remote remove origin 2>/dev/null
            git remote add origin "$github_url"
            echo -e "${GREEN}Remote set to: $github_url${NC}"
            
            echo -e "${BLUE}Do you want to push now? (y/n)${NC}"
            read push_now
            if [[ $push_now == "y" || $push_now == "Y" ]]; then
                git push -u origin main
            fi
        fi
        ;;
        
    4)
        echo "Exiting..."
        exit 0
        ;;
        
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Done!${NC}"
echo ""
echo -e "${BLUE}Your SAMS project is on GitHub!${NC}"
echo -e "Next steps:"
echo -e "1. Share the repository URL with your team"
echo -e "2. Set up GitHub Actions for CI/CD"
echo -e "3. Create issues for next features"
echo -e "4. Invite collaborators"
