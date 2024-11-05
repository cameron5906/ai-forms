interface LoadingButtonProps {
  loading?: boolean;
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  disabled?: boolean;
}

export const LoadingButton = ({
  loading,
  children,
  className,
  onClick,
  disabled,
}: LoadingButtonProps) => {
  return (
    <button
      className={className}
      onClick={onClick}
      disabled={disabled}
      style={{
        position: "relative",
        display: "inline-flex",
        alignItems: "center",
      }}
    >
      {loading && (
        <div className="spinner-container" style={{ marginRight: "0.5rem" }}>
          <div className="spinner"></div>
        </div>
      )}
      {children}
    </button>
  );
};
