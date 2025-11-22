"""
Course CLI
Command-line interface for managing courses
"""

import argparse
import sys
from typing import Optional

from src.utils.logging import get_logger


def create_course_command(args):
    """Cria um novo curso"""
    from src.main import initialize_system
    system = initialize_system(args.config)
    
    try:
        if args.url:
            source_type = "url"
            source_path = args.url
        elif args.file:
            source_type = "file"
            source_path = args.file
        elif args.directory:
            source_type = "directory"
            source_path = args.directory
        elif args.text:
            source_type = "text"
            source_path = args.text
        else:
            print("Error: Must specify --url, --file, --directory, or --text")
            sys.exit(1)
        
        course = system.create_course(
            name=args.name,
            description=args.description or "",
            source_type=source_type,
            source_path=source_path
        )
        
        print(f"Course created successfully!")
        print(f"ID: {course['id']}")
        print(f"Name: {course['name']}")
        print(f"Status: {course['status']}")
    
    finally:
        system.close()


def list_courses_command(args):
    """Lista todos os cursos"""
    from src.main import initialize_system
    system = initialize_system(args.config)
    
    try:
        courses = system.list_courses()
        
        if not courses:
            print("No courses found.")
            return
        
        print(f"\nFound {len(courses)} courses:\n")
        for course in courses:
            print(f"ID: {course['id']}")
            print(f"Name: {course['name']}")
            print(f"Status: {course.get('status', 'unknown')}")
            print(f"Source: {course.get('source_type', 'unknown')} - {course.get('source_path', 'N/A')}")
            print("-" * 50)
    
    finally:
        system.close()


def start_course_command(args):
    """Inicia aprendizado de um curso"""
    from src.main import initialize_system
    system = initialize_system(args.config)
    
    try:
        result = system.start_course_learning(args.course_id)
        
        if result.get('status') == 'success':
            print(f"Course {args.course_id} learning started successfully!")
            print(f"Chunks processed: {result.get('chunks_processed', 0)}")
            print(f"Concepts learned: {result.get('concepts_learned', 0)}")
        else:
            print(f"Error: {result.get('message', 'Unknown error')}")
            sys.exit(1)
    
    finally:
        system.close()


def status_course_command(args):
    """Mostra status de um curso"""
    from src.main import initialize_system
    system = initialize_system(args.config)
    
    try:
        status = system.get_course_status(args.course_id)
        
        print(f"\nCourse Status:")
        print(f"ID: {status['id']}")
        print(f"Name: {status['name']}")
        print(f"Status: {status['status']}")
        print(f"Content chunks: {status['content_chunks']}")
        print(f"Concepts learned: {status['concepts_learned']}")
        print(f"Created at: {status['created_at']}")
    
    finally:
        system.close()


def concepts_course_command(args):
    """Lista conceitos aprendidos de um curso"""
    from src.main import initialize_system
    system = initialize_system(args.config)
    
    try:
        concepts = system.get_course_concepts(args.course_id)
        
        if not concepts:
            print(f"No concepts learned for course {args.course_id}")
            return
        
        print(f"\nFound {len(concepts)} concepts:\n")
        for concept in concepts:
            print(f"Name: {concept['concept_name']}")
            print(f"Description: {concept.get('description', 'N/A')}")
            print(f"Confidence: {concept.get('confidence', 0.0):.2f}")
            if concept.get('examples'):
                print(f"Examples: {len(concept['examples'])}")
            print("-" * 50)
    
    finally:
        system.close()


def validate_course_command(args):
    """Valida um curso (manual ou automático)"""
    from src.main import initialize_system
    system = initialize_system(args.config)
    
    try:
        if args.automatic:
            # Validação automática
            result = system.validate_course(
                args.course_id,
                automatic=True,
                num_questions=args.num_questions,
                validation_threshold=args.threshold
            )
            
            if result.get('status') == 'passed':
                print(f"✅ Course {args.course_id} PASSED automatic validation!")
                print(f"   Average score: {result.get('average_score', 0):.2f}")
                print(f"   Threshold: {result.get('validation_threshold', 0):.2f}")
                print(f"   Questions answered: {result.get('num_questions', 0)}")
            else:
                print(f"❌ Course {args.course_id} FAILED automatic validation")
                print(f"   Average score: {result.get('average_score', 0):.2f}")
                print(f"   Threshold: {result.get('validation_threshold', 0):.2f}")
                print(f"   Questions answered: {result.get('num_questions', 0)}")
                sys.exit(1)
        else:
            # Validação manual
            result = system.validate_course(args.course_id, automatic=False)
            
            if result.get('status') == 'validated':
                print(f"Course {args.course_id} marked as validated!")
            else:
                print(f"Error: {result.get('message', 'Unknown error')}")
                sys.exit(1)
    
    finally:
        system.close()


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="npllm Course Management CLI")
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new course')
    create_parser.add_argument('--name', required=True, help='Course name')
    create_parser.add_argument('--description', help='Course description')
    create_parser.add_argument('--url', help='Source URL')
    create_parser.add_argument('--file', help='Source file path')
    create_parser.add_argument('--directory', help='Source directory path')
    create_parser.add_argument('--text', help='Source text (direct input)')
    create_parser.set_defaults(func=create_course_command)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all courses')
    list_parser.set_defaults(func=list_courses_command)
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start course learning')
    start_parser.add_argument('course_id', type=int, help='Course ID')
    start_parser.set_defaults(func=start_course_command)
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show course status')
    status_parser.add_argument('course_id', type=int, help='Course ID')
    status_parser.set_defaults(func=status_course_command)
    
    # Concepts command
    concepts_parser = subparsers.add_parser('concepts', help='List learned concepts')
    concepts_parser.add_argument('course_id', type=int, help='Course ID')
    concepts_parser.set_defaults(func=concepts_course_command)
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a course')
    validate_parser.add_argument('course_id', type=int, help='Course ID')
    validate_parser.add_argument(
        '--automatic',
        action='store_true',
        help='Use automatic validation (generates questions and validates answers)'
    )
    validate_parser.add_argument(
        '--num-questions',
        type=int,
        default=10,
        help='Number of questions for automatic validation (default: 10)'
    )
    validate_parser.add_argument(
        '--threshold',
        type=float,
        default=0.75,
        help='Validation threshold (0.0 to 1.0, default: 0.75)'
    )
    validate_parser.set_defaults(func=validate_course_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()

